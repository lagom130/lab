package io.github.lagom130.lab.common.feign

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class CommonFeignApplication

fun main(args: Array<String>) {
    runApplication<CommonFeignApplication>(*args)
}
