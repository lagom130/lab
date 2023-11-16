package io.github.logom130.lab.globalResponse

data class GlobalResult<T>(val code: Int = 0, val msg: String?, val data: T?)
