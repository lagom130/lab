package io.github130.lab.cat.globalResponse

data class Result<T>(val code: Int = 0, val msg: String? = "操作成功", val data: T?)
