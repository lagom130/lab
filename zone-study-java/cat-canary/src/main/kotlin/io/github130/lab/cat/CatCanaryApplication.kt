package io.github130.lab.cat

import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.context.annotation.Bean
import org.springframework.web.servlet.view.json.MappingJackson2JsonView

@SpringBootApplication
class CatCanaryApplication

fun main(args: Array<String>) {
	runApplication<CatCanaryApplication>(*args)
}

@Bean
fun json(): MappingJackson2JsonView {
	return MappingJackson2JsonView(ObjectMapper())
}