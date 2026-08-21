#!/usr/bin/env bash
# Source this inside Lightning Studio before running PowerX V2.
export POWERX_REGISTRY_PATH="${POWERX_REGISTRY_PATH:-config/powerx_v2_model_registry.json}"
export POWERX_WAREHOUSE_ROOT="${POWERX_WAREHOUSE_ROOT:-/teamspace/studios/this_studio/PowerXWarehouse}"
export POWERX_CACHE_ROOT="${POWERX_CACHE_ROOT:-/teamspace/studios/this_studio/.powerx_cache}"
export POWERX_MOCK_MODE="${POWERX_MOCK_MODE:-1}"
export POWERX_V2_API_KEY="${POWERX_V2_API_KEY:-change-me}"
echo "POWERX_WAREHOUSE_ROOT=$POWERX_WAREHOUSE_ROOT"
echo "POWERX_CACHE_ROOT=$POWERX_CACHE_ROOT"
echo "POWERX_MOCK_MODE=$POWERX_MOCK_MODE"
