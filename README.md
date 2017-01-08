# CVXPY-CODEGEN

**WARNING:** This tool is still in an early stage of development, and many bugs might still exist.  Consider it an early alpha, and don't use it for safety-critical applications (yet).

cvxpy-codegen generates embedded C code for solving convex optimization problems.  It allows the user to specify a family of convex optimization problems at a high abstraction level using Python, and then solve instances of this problem family in C (possibly on an embedded microcontroller.) CVXPY-CODEGEN uses CVXPY as a front end for specifying the convex optimization problem.  The generated C code calls an embedded solver (currently ECOS) to solve the problem.

Abstractly, cvxpy-codegen addresses parametrized *families* of convex optimization problems of the form:

    minimize    f_0(x, a)
    subject to  f_i(x, a) <= 0, for i = 1,...,m.

Within this family of problems, the parameter `a` defines a specific problem instance; for every such problem instance, the variable `x` is to be determined by solving the optimization problem.  In CVXPY-CODEGEN, the problem family (*ie*, the functions f_i) are specified in Python using CVXPY.  After C code is generated for this family, the user passes in the parameter `a`, and the problem is solved (all in C).  Currently, problems handled include least squares problems, linear programs (LPs), quadratic programs (QPs), second-order cone programs (SOCPs).

#### Least squares example
To make this all concrete, let's try a simple least-squares problem:

    import cvxpy_codegen as cg
    A = cg.Parameter(m, n, name='A')
    b = cg.Parameter(m, name='b')
    x = cg.Variable(n, name='x')
    f0 = cg.norm(A*x - b)
    prob = cg.Problem(cg.Minimize(f0))
    prob.codegen('~/least_squares_example')

Then the generated code is available in the `~/least_squares_example` directory.  The API is contained in the header file `codegen.h`.  To test out the embedded solver on randomly generated data,

    cd ~/least_squares_example
    make
    ./test_solver

If you'd rather not use random data, you can specify the data to be used by adding 

    import numpy as np
    A.value = np.random.randn(m, n)
    b.value = np.random.randn(m, 1)

before generating the C code in Python.

The directory also contains a Python wrapper, so you can use your embedded C solver in Python as a C exension (The default name of this extension is `cvxpy_codegen_solver`.)
