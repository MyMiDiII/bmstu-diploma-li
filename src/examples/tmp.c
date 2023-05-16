#include <stdio.h>
#include <Python.h>

int main()
{
    Py_Initialize();
    PyObject* module = PyImport_ImportModule("indexes.builder");
    printf("%p\n", (void *)module);

    PyObject* className = PyObject_GetAttrString(module, "LindexBuilder");
    printf("%p\n", (void *)className);
    PyObject* args = PyTuple_Pack(1, PyUnicode_FromString("fcnn2"));
    PyObject* instance = PyObject_CallObject(className, args);
    printf("%p\n", (void *)instance);

    PyObject* lindex = PyObject_CallMethod(instance, "build", NULL);
    PyObject_CallMethod(lindex, "success", NULL);

    Py_DECREF(instance);
    Py_DECREF(className);
    Py_DECREF(module);
    Py_Finalize();
}

