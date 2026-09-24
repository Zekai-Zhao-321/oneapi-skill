// A small correctness test. Select a device class explicitly; never fall back.
#include <sycl/sycl.hpp>
#include <atomic>
#include <cstddef>
#include <exception>
#include <iostream>
#include <string>

int main(int argc, char **argv) {
    if (argc != 3 || std::string(argv[1]) != "--device" ||
        (std::string(argv[2]) != "gpu" && std::string(argv[2]) != "cpu")) {
        std::cerr << "Usage: sycl-smoke --device gpu|cpu\n";
        return 2;
    }
    std::atomic<bool> async_failed{false};
    try {
        const sycl::device device = std::string(argv[2]) == "gpu"
            ? sycl::device{sycl::gpu_selector_v} : sycl::device{sycl::cpu_selector_v};
        sycl::queue queue{device, [&async_failed](sycl::exception_list errors) {
            async_failed.store(true);
            for (const auto &error : errors) {
                try { std::rethrow_exception(error); }
                catch (const std::exception &e) { std::cerr << "Async error: " << e.what() << '\n'; }
                catch (...) { std::cerr << "Unknown asynchronous error\n"; }
            }
        }};
        std::cout << "device=" << device.get_info<sycl::info::device::name>()
                  << "\nvendor=" << device.get_info<sycl::info::device::vendor>()
                  << "\nplatform=" << device.get_platform().get_info<sycl::info::platform::name>()
                  << "\ndriver=" << device.get_info<sycl::info::device::driver_version>()
                  << "\nbackend_id=" << static_cast<int>(queue.get_backend()) << '\n';
        constexpr std::size_t count = 4096;
        {
            sycl::buffer<int, 1> result{sycl::range<1>{count}};
            queue.submit([&](sycl::handler &handler) {
                sycl::accessor output{result, handler, sycl::write_only, sycl::no_init};
                handler.parallel_for(sycl::range<1>{count}, [=](sycl::id<1> i) {
                    output[i] = static_cast<int>(i[0]) * 3 + 7;
                });
            });
            queue.wait_and_throw();
            if (async_failed.load()) return 1;
            sycl::host_accessor output{result, sycl::read_only};
            for (std::size_t i = 0; i < count; ++i) {
                if (output[i] != static_cast<int>(i) * 3 + 7) {
                    std::cerr << "Mismatch at " << i << ": " << output[i] << '\n';
                    return 1;
                }
            }
        }
        queue.wait_and_throw();
        if (async_failed.load()) return 1;
        std::cout << "PASS: checked " << count << " elements on requested " << argv[2] << '\n';
        return 0;
    } catch (const std::exception &e) {
        std::cerr << "FAIL: " << e.what() << '\n';
        return 1;
    }
}
