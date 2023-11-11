package io.github130.lab.cat.service.impl

import io.github130.lab.cat.service.IHelloService
import org.springframework.stereotype.Service

@Service
class HelloServiceImpl : IHelloService {
    val say = "hello "
    override fun hello(name: String): String {
        return say + name
    }
}