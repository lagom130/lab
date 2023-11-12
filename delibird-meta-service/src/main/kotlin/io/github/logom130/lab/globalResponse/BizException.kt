package io.github130.lab.cat.globalResponse

class BizException(var errorCode: Int, var errorMsg: String) : RuntimeException()
