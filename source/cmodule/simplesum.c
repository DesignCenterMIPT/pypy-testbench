#include <Python.h>

static PyObject *simple_sum(PyObject *self, PyObject *args) {
  long a, b = -1;
  /* Parse arguments */
  if (!PyArg_ParseTuple(args, "ll", &a, &b)) {
    return NULL;
  }
  return PyLong_FromLong(a+b);
}

// non-returning version
static PyObject *simple_sum_noret(PyObject *self, PyObject *args) {
  long a, b = -1;
  /* Parse arguments */
  if (!PyArg_ParseTuple(args, "ll", &a, &b)) {
    return NULL;
  }
  a = a + b;
  Py_RETURN_NONE;
}

static PyObject *simple_sum_noret2(PyObject *self, PyObject *arg)
{
  long a = -1;
  /* Parse arguments */
#if !defined(PYPY_VERSION)
  if (!PyArg_ParseTuple(arg, "l", &a))
  {
    return NULL;
  }
#else
  a = *(long*)(arg+28);
#endif
  a = a;
  // return value just for checking it, replace with:
  // Py_RETURN_NONE;
  return PyLong_FromLong(a);
}
static PyMethodDef SimpleSumMethods[] = {
    {"SimpleSum", simple_sum, METH_VARARGS, "Python interface for Simple Sum function"},
    {"SimpleSumNr", simple_sum_noret, METH_VARARGS, "Python interface for Simple Sum function (non-returning)"},
    {"SimpleSumNr2", simple_sum_noret2, METH_VARARGS_W, "Python interface for Simple Sum function (non-returning) #2"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef SimpleSumModule = {
    PyModuleDef_HEAD_INIT,
    "SimpleSum",
    "Python interface for the Simple Sum function",
    -1,
    SimpleSumMethods
};

PyMODINIT_FUNC PyInit_simplesum(void) {
    return PyModule_Create(&SimpleSumModule);
}
