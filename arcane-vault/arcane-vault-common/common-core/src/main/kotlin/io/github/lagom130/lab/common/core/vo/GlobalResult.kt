package io.github.lagom130.lab.common.core.vo

data class GlobalResult<T>(val code: Int = 0, val msg: String?, val data: T?)
