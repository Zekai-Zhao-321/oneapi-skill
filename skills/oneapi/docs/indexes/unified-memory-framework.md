# unified-memory-framework

Upstream: https://github.com/oneapi-src/unified-memory-framework/tree/19ce12f5f40213a612828e32a3b1d1b857222312

Paths preserve the upstream layout. API and example files can also be found with search_docs.py --kind all.

## doc

- [README.md](../upstream/unified-memory-framework/README.md)
- [docs/README.md](../upstream/unified-memory-framework/docs/README.md)
- [docs/config/api.rst](../upstream/unified-memory-framework/docs/config/api.rst)
- [docs/config/ctl.rst](../upstream/unified-memory-framework/docs/config/ctl.rst)
- [docs/config/examples.rst](../upstream/unified-memory-framework/docs/config/examples.rst)
- [docs/config/glossary.rst](../upstream/unified-memory-framework/docs/config/glossary.rst)
- [docs/config/index.rst](../upstream/unified-memory-framework/docs/config/index.rst)
- [docs/config/introduction.rst](../upstream/unified-memory-framework/docs/config/introduction.rst)
- [examples/README.md](../upstream/unified-memory-framework/examples/README.md)

## api

- [include/umf.h](../upstream/unified-memory-framework/include/umf.h)
- [include/umf/base.h](../upstream/unified-memory-framework/include/umf/base.h)
- [include/umf/experimental/ctl.h](../upstream/unified-memory-framework/include/umf/experimental/ctl.h)
- [include/umf/experimental/memory_properties.h](../upstream/unified-memory-framework/include/umf/experimental/memory_properties.h)
- [include/umf/experimental/mempolicy.h](../upstream/unified-memory-framework/include/umf/experimental/mempolicy.h)
- [include/umf/experimental/memspace.h](../upstream/unified-memory-framework/include/umf/experimental/memspace.h)
- [include/umf/experimental/memtarget.h](../upstream/unified-memory-framework/include/umf/experimental/memtarget.h)
- [include/umf/ipc.h](../upstream/unified-memory-framework/include/umf/ipc.h)
- [include/umf/memory_pool.h](../upstream/unified-memory-framework/include/umf/memory_pool.h)
- [include/umf/memory_pool_ops.h](../upstream/unified-memory-framework/include/umf/memory_pool_ops.h)
- [include/umf/memory_provider.h](../upstream/unified-memory-framework/include/umf/memory_provider.h)
- [include/umf/memory_provider_gpu.h](../upstream/unified-memory-framework/include/umf/memory_provider_gpu.h)
- [include/umf/memory_provider_ops.h](../upstream/unified-memory-framework/include/umf/memory_provider_ops.h)
- [include/umf/pools/pool_disjoint.h](../upstream/unified-memory-framework/include/umf/pools/pool_disjoint.h)
- [include/umf/pools/pool_jemalloc.h](../upstream/unified-memory-framework/include/umf/pools/pool_jemalloc.h)
- [include/umf/pools/pool_proxy.h](../upstream/unified-memory-framework/include/umf/pools/pool_proxy.h)
- [include/umf/pools/pool_scalable.h](../upstream/unified-memory-framework/include/umf/pools/pool_scalable.h)
- [include/umf/providers/provider_cuda.h](../upstream/unified-memory-framework/include/umf/providers/provider_cuda.h)
- [include/umf/providers/provider_devdax_memory.h](../upstream/unified-memory-framework/include/umf/providers/provider_devdax_memory.h)
- [include/umf/providers/provider_file_memory.h](../upstream/unified-memory-framework/include/umf/providers/provider_file_memory.h)
- [include/umf/providers/provider_fixed_memory.h](../upstream/unified-memory-framework/include/umf/providers/provider_fixed_memory.h)
- [include/umf/providers/provider_level_zero.h](../upstream/unified-memory-framework/include/umf/providers/provider_level_zero.h)
- [include/umf/providers/provider_os_memory.h](../upstream/unified-memory-framework/include/umf/providers/provider_os_memory.h)
- [include/umf/proxy_lib_new_delete.h](../upstream/unified-memory-framework/include/umf/proxy_lib_new_delete.h)

## example

- [examples/CMakeLists.txt](../upstream/unified-memory-framework/examples/CMakeLists.txt)
- [examples/basic/CMakeLists.txt](../upstream/unified-memory-framework/examples/basic/CMakeLists.txt)
- [examples/basic/basic.c](../upstream/unified-memory-framework/examples/basic/basic.c)
- [examples/cmake/FindCUDA.cmake](../upstream/unified-memory-framework/examples/cmake/FindCUDA.cmake)
- [examples/cmake/FindJEMALLOC.cmake](../upstream/unified-memory-framework/examples/cmake/FindJEMALLOC.cmake)
- [examples/cmake/FindLIBHWLOC.cmake](../upstream/unified-memory-framework/examples/cmake/FindLIBHWLOC.cmake)
- [examples/cmake/FindLIBNUMA.cmake](../upstream/unified-memory-framework/examples/cmake/FindLIBNUMA.cmake)
- [examples/cmake/FindLIBUMF.cmake](../upstream/unified-memory-framework/examples/cmake/FindLIBUMF.cmake)
- [examples/cmake/FindTBB.cmake](../upstream/unified-memory-framework/examples/cmake/FindTBB.cmake)
- [examples/cmake/FindZE_LOADER.cmake](../upstream/unified-memory-framework/examples/cmake/FindZE_LOADER.cmake)
- [examples/common/examples_level_zero_helpers.c](../upstream/unified-memory-framework/examples/common/examples_level_zero_helpers.c)
- [examples/common/examples_level_zero_helpers.h](../upstream/unified-memory-framework/examples/common/examples_level_zero_helpers.h)
- [examples/common/examples_utils.h](../upstream/unified-memory-framework/examples/common/examples_utils.h)
- [examples/ctl/CMakeLists.txt](../upstream/unified-memory-framework/examples/ctl/CMakeLists.txt)
- [examples/ctl/ctl.c](../upstream/unified-memory-framework/examples/ctl/ctl.c)
- [examples/ctl/custom_ctl.c](../upstream/unified-memory-framework/examples/ctl/custom_ctl.c)
- [examples/cuda_shared_memory/CMakeLists.txt](../upstream/unified-memory-framework/examples/cuda_shared_memory/CMakeLists.txt)
- [examples/cuda_shared_memory/cuda_shared_memory.c](../upstream/unified-memory-framework/examples/cuda_shared_memory/cuda_shared_memory.c)
- [examples/custom_file_provider/CMakeLists.txt](../upstream/unified-memory-framework/examples/custom_file_provider/CMakeLists.txt)
- [examples/custom_file_provider/custom_file_provider.c](../upstream/unified-memory-framework/examples/custom_file_provider/custom_file_provider.c)
- [examples/dram_and_fsdax/CMakeLists.txt](../upstream/unified-memory-framework/examples/dram_and_fsdax/CMakeLists.txt)
- [examples/dram_and_fsdax/dram_and_fsdax.c](../upstream/unified-memory-framework/examples/dram_and_fsdax/dram_and_fsdax.c)
- [examples/fetch_content/CMakeLists.txt](../upstream/unified-memory-framework/examples/fetch_content/CMakeLists.txt)
- [examples/fetch_content/fetch_umf.cmake](../upstream/unified-memory-framework/examples/fetch_content/fetch_umf.cmake)
- [examples/ipc_ipcapi/CMakeLists.txt](../upstream/unified-memory-framework/examples/ipc_ipcapi/CMakeLists.txt)
- [examples/ipc_ipcapi/ipc_ipcapi_anon_fd.sh](../upstream/unified-memory-framework/examples/ipc_ipcapi/ipc_ipcapi_anon_fd.sh)
- [examples/ipc_ipcapi/ipc_ipcapi_consumer.c](../upstream/unified-memory-framework/examples/ipc_ipcapi/ipc_ipcapi_consumer.c)
- [examples/ipc_ipcapi/ipc_ipcapi_producer.c](../upstream/unified-memory-framework/examples/ipc_ipcapi/ipc_ipcapi_producer.c)
- [examples/ipc_ipcapi/ipc_ipcapi_shm.sh](../upstream/unified-memory-framework/examples/ipc_ipcapi/ipc_ipcapi_shm.sh)
- [examples/ipc_level_zero/CMakeLists.txt](../upstream/unified-memory-framework/examples/ipc_level_zero/CMakeLists.txt)
- [examples/ipc_level_zero/ipc_level_zero.c](../upstream/unified-memory-framework/examples/ipc_level_zero/ipc_level_zero.c)
- [examples/level_zero_shared_memory/CMakeLists.txt](../upstream/unified-memory-framework/examples/level_zero_shared_memory/CMakeLists.txt)
- [examples/level_zero_shared_memory/level_zero_shared_memory.c](../upstream/unified-memory-framework/examples/level_zero_shared_memory/level_zero_shared_memory.c)
- [examples/memspace_hmat/CMakeLists.txt](../upstream/unified-memory-framework/examples/memspace_hmat/CMakeLists.txt)
- [examples/memspace_hmat/memspace_hmat.c](../upstream/unified-memory-framework/examples/memspace_hmat/memspace_hmat.c)
- [examples/memspace_numa/CMakeLists.txt](../upstream/unified-memory-framework/examples/memspace_numa/CMakeLists.txt)
- [examples/memspace_numa/memspace_numa.c](../upstream/unified-memory-framework/examples/memspace_numa/memspace_numa.c)

## license

- [LICENSE.TXT](../upstream/unified-memory-framework/LICENSE.TXT)
- [licensing/third-party-programs.txt](../upstream/unified-memory-framework/licensing/third-party-programs.txt)

## support

- [docs/config/conf.py](../upstream/unified-memory-framework/docs/config/conf.py)
- [docs/generate_docs.py](../upstream/unified-memory-framework/docs/generate_docs.py)

