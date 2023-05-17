#include <stdio.h>
#include <Python.h>

int main()
{
    Py_Initialize();
    PyObject* builderModule = PyImport_ImportModule("indexes.builder");
    printf("%p\n", (void *)builderModule);

    PyObject* builderClassName= PyObject_GetAttrString(builderModule, "LindexBuilder");
    printf("%p\n", (void *)builderClassName);
    PyObject* modelName = PyTuple_Pack(1, PyUnicode_FromString("fcnn2"));
    PyObject* builder = PyObject_CallObject(builderClassName, modelName);
    printf("%p\n", (void *)builder);

    PyObject* lindex = PyObject_CallMethod(builder, "build", NULL);

    int cKeys[10] = {5, 3, 9, 4, 2, 10, 1, 0, 45, 6};
    PyObject* keys = PyList_New(0);
    PyObject* rows = PyList_New(0);

    for (int i = 0; i < 10; ++i)
    {
        PyList_Append(keys, PyLong_FromLong(cKeys[i]));
        PyList_Append(rows, PyLong_FromLong(i));
    }

    PyObject* train = PyUnicode_FromString("train");

    PyObject* check = PyObject_CallMethodObjArgs(lindex, train, keys, rows, NULL);

    if (!check)
    {
        puts("OH NO!");
        PyErr_Print();
        PyErr_Clear();
    }

    Py_DECREF(train);
    Py_DECREF(keys);
    Py_DECREF(rows);
    Py_DECREF(lindex);
    Py_DECREF(builder);
    Py_DECREF(modelName);
    Py_DECREF(builderClassName);
    Py_DECREF(builderModule);
    Py_Finalize();
}

