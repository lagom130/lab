package io.github.lagom130.lab.common.web.utils

import io.github.lagom130.lab.common.web.vo.GlobalResult

class ResultUtils<T> {
    companion object{
        fun fail(code:Int, message:String): GlobalResult<*> {
            return GlobalResult(code,message,null)
        }
        fun success(): GlobalResult<*> {
            return GlobalResult(200,"操作成功",null)
        }

        fun <T> success(data: T): GlobalResult<T> {
            return GlobalResult(200, "操作成功", data)
        }
    }
}