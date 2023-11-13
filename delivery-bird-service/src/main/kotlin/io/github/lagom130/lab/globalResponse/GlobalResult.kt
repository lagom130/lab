package io.github130.lab.cat.globalResponse

data class GlobalResult<T>(val code: Int = 0, val msg: String?, val data: T?)
