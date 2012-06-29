/*
 * Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

#ifndef IP_CONNECTION
#define IP_CONNECTION

#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#if !defined __cplusplus && defined __GNUC__
	#include <stdbool.h>
#endif

#ifdef _WIN32
	#ifndef WIN32_LEAN_AND_MEAN
		#define WIN32_LEAN_AND_MEAN
	#endif
	#include <windows.h>
	#include <winsock2.h>
#else
	#include <netinet/in.h> // struct sockaddr_in
	#include <pthread.h>
	#include <semaphore.h>
#endif

#define E_OK 0
#define E_TIMEOUT -1
#define E_NO_STREAM_SOCKET -2
#define E_HOSTNAME_INVALID -3
#define E_NO_CONNECT -4
#define E_NO_THREAD -5
#define E_NOT_ADDED -6

#define RESPONSE_TIMEOUT 2500

#define MAX_LENGTH_NAME 40

#define MAX_NUM_DEVICES 256
#define MAX_NUM_CALLBACKS 256
#define MAX_PACKET_SIZE 4096
#define RECV_BUFFER_SIZE (MAX_PACKET_SIZE * 2)

#define BROADCAST_ADDRESS 0

#define FUNCTION_GET_STACK_ID 255
#define FUNCTION_ENUMERATE 254
#define FUNCTION_ENUMERATE_CALLBACK 253

struct IPConnection_;
struct Device_;

typedef void (*enumerate_callback_func_t)(char*, char*, uint8_t, bool);
typedef int (*device_callback_func_t)(struct Device_*, const unsigned char*);

typedef struct {
	uint8_t function_id;
	uint16_t length;
	char buffer[MAX_PACKET_SIZE];
} DeviceResponse;

typedef struct Device_{
	uint8_t stack_id;
	uint64_t uid;
#ifdef _WIN32
	CRITICAL_SECTION write_mutex;
	HANDLE response_semaphore;
#else
	pthread_mutex_t write_mutex;
	pthread_cond_t response_cond;
	bool response_flag;
	pthread_mutex_t response_mutex;
#endif
	const char *expected_name;
	char name[MAX_LENGTH_NAME];
	uint8_t firmware_version[3];
	uint8_t binding_version[3];
	DeviceResponse response;
	void *registered_callbacks[MAX_NUM_CALLBACKS];
	device_callback_func_t callback_wrappers[MAX_NUM_CALLBACKS];
	struct IPConnection_ *ipcon;
} Device;

typedef struct CallbackQueueNode_{
	struct CallbackQueueNode_ *next;
	unsigned char buffer[1];
} CallbackQueueNode;

typedef struct IPConnection_{
#ifdef _WIN32
	SOCKET s;
	HANDLE thread_receive;
	HANDLE thread_callback;
#else
	int fd;
	pthread_t thread_receive;
	pthread_t thread_callback;
#endif
	bool thread_run_flag;
	struct sockaddr_in server;
	Device *devices[MAX_NUM_DEVICES];
	Device *pending_add_device;
	enumerate_callback_func_t enumerate_callback;
	CallbackQueueNode *callback_queue_head;
	CallbackQueueNode *callback_queue_tail;
#ifdef _WIN32
	CRITICAL_SECTION callback_queue_mutex;
	HANDLE callback_queue_semaphore;
#else
	pthread_mutex_t callback_queue_mutex;
	sem_t callback_queue_semaphore_object;
	sem_t *callback_queue_semaphore;
#endif
} IPConnection;

#if defined _MSC_VER || defined __BORLANDC__
	#pragma pack(push)
	#pragma pack(1)
	#define ATTRIBUTE_PACKED
#elif defined __GNUC__
	#define ATTRIBUTE_PACKED __attribute__((packed))
#else
	#error unknown compiler, do not know how to enable struct packing
#endif

typedef struct {
	uint8_t stack_id;
	uint8_t function_id;
	uint16_t length;
	uint64_t uid;
} ATTRIBUTE_PACKED GetStackID;

typedef struct {
	uint8_t stack_id;
	uint8_t function_id;
	uint16_t length;
	uint64_t device_uid;
	uint8_t device_firmware_version[3];
	char device_name[MAX_LENGTH_NAME];
	uint8_t device_stack_id;
} ATTRIBUTE_PACKED GetStackIDReturn;

typedef struct {
	uint8_t stack_id;
	uint8_t function_id;
	uint16_t length;
} ATTRIBUTE_PACKED Enumerate;

typedef struct {
	uint8_t stack_id;
	uint8_t function_id;
	uint16_t length;
	uint64_t device_uid;
	char device_name[MAX_LENGTH_NAME];
	uint8_t device_stack_id;
	bool is_new;
} ATTRIBUTE_PACKED EnumerateReturn;

#if defined _MSC_VER || defined __BORLANDC__
	#pragma pack(pop)
#endif
#undef ATTRIBUTE_PACKED

#ifdef _WIN32
void ipcon_mutex_lock(CRITICAL_SECTION *mutex);
void ipcon_mutex_unlock(CRITICAL_SECTION *mutex);
#else
void ipcon_mutex_lock(pthread_mutex_t *mutex);
void ipcon_mutex_unlock(pthread_mutex_t *mutex);
#endif

int ipcon_create(IPConnection *ipcon, const char *host, const int port);
void ipcon_enumerate(IPConnection *ipcon, enumerate_callback_func_t callback);
int ipcon_add_device(IPConnection *ipcon, Device *device);
void ipcon_join_thread(IPConnection *ipcon);
void ipcon_destroy(IPConnection *ipcon);

void ipcon_base58encode(uint64_t value, char *str);
uint64_t ipcon_base58decode(const char *str);

#ifdef _WIN32
void ipcon_recv_loop(void *param);
#else
void *ipcon_recv_loop(void *param);
#endif
void ipcon_handle_enumerate(IPConnection *ipcon, const unsigned char *buffer);
void ipcon_handle_message(IPConnection *ipcon, const unsigned char *buffer);
void ipcon_device_write(Device *device, const char *buffer, const int length);
void ipcon_device_create(Device *device, const char *uid);
void ipcon_handle_add_device(IPConnection *ipcon,
                             const unsigned char *buffer);
int ipcon_device_expect_response(Device *device);

uint8_t ipcon_get_stack_id_from_data(const unsigned char *data);
uint8_t ipcon_get_function_id_from_data(const unsigned char *data);
uint16_t ipcon_get_length_from_data(const unsigned char *data);

#endif
