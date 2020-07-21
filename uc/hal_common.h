/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_HAL_COMMON_H
#define TF_HAL_COMMON_H

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <stdarg.h>

#include "config.h"
#include "packetbuffer.h"
#include "macros.h"

#ifdef __cplusplus
extern "C" {
#endif

struct TF_TfpContext;

typedef struct TF_HalCommon {
    //TF_INVENTORY_SIZE + 1 for the unknown bricklet used for device discovery
    uint32_t uids[TF_INVENTORY_SIZE + 1];
    uint8_t port_ids[TF_INVENTORY_SIZE + 1];
    struct TF_TfpContext *tfps[TF_INVENTORY_SIZE + 1];
    uint16_t dids[TF_INVENTORY_SIZE + 1];
    size_t used;

    uint32_t timeout;

    bool callback_executing;
    uint8_t port_count;
    size_t callback_tick_index;
} TF_HalCommon;

typedef struct TF_HalContext TF_HalContext;

void tf_hal_set_timeout(TF_HalContext *hal, uint32_t timeout_us) TF_ATTRIBUTE_NONNULL;
uint32_t tf_hal_get_timeout(TF_HalContext *hal) TF_ATTRIBUTE_NONNULL;
bool tf_hal_get_device_info(TF_HalContext *hal, size_t index, char ret_uid[7], char *ret_port_name, uint16_t *ret_device_id) TF_ATTRIBUTE_NONNULL TF_ATTRIBUTE_WARN_UNUSED_RESULT;
int tf_hal_callback_tick(TF_HalContext *hal, uint32_t timeout_us) TF_ATTRIBUTE_NONNULL;

#define TF_LOG_LEVEL_NONE 0
#define TF_LOG_LEVEL_ERROR 1
#define TF_LOG_LEVEL_INFO 2
#define TF_LOG_LEVEL_DEBUG 3

#if TF_LOG_LEVEL >= TF_LOG_LEVEL_ERROR
#define tf_hal_log_error(...) tf_hal_log_formatted_message(__VA_ARGS__)
#else
#define tf_hal_log_error(...)
#endif

#if TF_LOG_LEVEL >= TF_LOG_LEVEL_INFO
#define tf_hal_log_info(...) tf_hal_log_formatted_message(__VA_ARGS__)
#else
#define tf_hal_log_info(...)
#endif

#if TF_LOG_LEVEL >= TF_LOG_LEVEL_DEBUG
#define tf_hal_log_debug(...) tf_hal_log_formatted_message(__VA_ARGS__)
#else
#define tf_hal_log_debug(...)
#endif

void tf_hal_log_formatted_message(const char *format, ...) TF_ATTRIBUTE_NONNULL;

// To be used by HAL implementations
int tf_hal_common_init(TF_HalContext *hal) TF_ATTRIBUTE_NONNULL TF_ATTRIBUTE_WARN_UNUSED_RESULT;
int tf_hal_finish_init(TF_HalContext *hal, uint8_t port_count, uint32_t port_discovery_timeout_us) TF_ATTRIBUTE_NONNULL TF_ATTRIBUTE_WARN_UNUSED_RESULT;
int tf_hal_get_port_id(TF_HalContext *hal, uint32_t uid, uint8_t *port_id, int *inventory_index) TF_ATTRIBUTE_NONNULL TF_ATTRIBUTE_WARN_UNUSED_RESULT;
bool tf_hal_enumerate_handler(TF_HalContext *hal, uint8_t port_id, TF_Packetbuffer *payload) TF_ATTRIBUTE_NONNULL TF_ATTRIBUTE_WARN_UNUSED_RESULT;


// BEGIN - To be implemented by the specific HAL
int tf_hal_destroy(TF_HalContext *hal) TF_ATTRIBUTE_NONNULL;
int tf_hal_chip_select(TF_HalContext *hal, uint8_t port_id, bool enable) TF_ATTRIBUTE_NONNULL TF_ATTRIBUTE_WARN_UNUSED_RESULT;
int tf_hal_transceive(TF_HalContext *hal, uint8_t port_id, const uint8_t *write_buffer, uint8_t *read_buffer, uint32_t length) TF_ATTRIBUTE_NONNULL TF_ATTRIBUTE_WARN_UNUSED_RESULT;
uint32_t tf_hal_current_time_us(TF_HalContext *hal) TF_ATTRIBUTE_NONNULL;
void tf_hal_sleep_us(TF_HalContext *hal, uint32_t us) TF_ATTRIBUTE_NONNULL;
TF_HalCommon *tf_hal_get_common(TF_HalContext *hal) TF_ATTRIBUTE_NONNULL;
char tf_hal_get_port_name(TF_HalContext *hal, uint8_t port_id) TF_ATTRIBUTE_NONNULL;

// These functions have to work without an initialized HAL to be able to report HAL initialization info/errors, so don't pass the handle here.
void tf_hal_log_message(const char *msg) TF_ATTRIBUTE_NONNULL;
const char *tf_hal_strerror(int rc);

// END - To be implemented by the specific HAL

#ifdef __cplusplus
}
#endif

#endif
