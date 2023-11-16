package io.github.lagom130.lab.common.core.exception

class BizException(var errorCode: Int, var errorMsg: String) : RuntimeException()
