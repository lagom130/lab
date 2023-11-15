package io.github.logom130.lab.globalResponse

class BizException(var errorCode: Int, var errorMsg: String) : RuntimeException()
