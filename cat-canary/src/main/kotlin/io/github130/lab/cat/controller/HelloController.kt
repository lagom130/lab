package io.github130.lab.cat.controller

import io.github130.lab.cat.globalResponse.GlobalResult
import io.github130.lab.cat.service.IHelloService
import jakarta.annotation.Resource
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

/**
 * default controller
 *
 * @author lujc
 * @date 2023/11/11.
 */
@RestController
@RequestMapping("/hello")
class HelloController {
    @Resource
    private lateinit var helloService: IHelloService

    @GetMapping("/{name}")
    fun hello(@PathVariable name: String): GlobalResult<String> {
        return GlobalResult(200,"操作成功", helloService.hello(name))
    }
}