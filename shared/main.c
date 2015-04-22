#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>

void * loadMyLibs(void) {
    int i, j;
    void *handle;
    char *error;
    int (*test_a)(void);
    int (*test_b)(void);

    handle = dlopen ("./libmystuff.so.1.0.1", RTLD_LAZY);
    if(!handle) {
        fputs(dlerror(), stderr);
        exit(1);
    }

    test_a = dlsym(handle, "test_a");
    if (( error = dlerror()) != NULL ) {
        fputs(error, stderr);
        exit(1);
    }

    test_b = dlsym(handle, "test_b");
    if (( error = dlerror()) != NULL ) {
        fputs(error, stderr);
        exit(1);
    }
    
    i = (*test_a)();
    j = (*test_b)();
    printf("%d, %d\n", i, j);

    dlclose(handle);
    return 0;
    
}

int main(void) {

  loadMyLibs();

  return 0;
}
