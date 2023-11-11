package io.github130.lab.cat.controller

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
@RequestMapping("/default")
class DefaultController {

    @GetMapping("/hello/{name}")
    fun hello(@PathVariable name: String): String {
        return "hello $name"
    }
}