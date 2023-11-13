package io.github.lagom130.lab

import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.context.annotation.Bean
import org.springframework.web.servlet.view.json.MappingJackson2JsonView

@SpringBootApplication
class DelibirdMetaApplication

fun main(args: Array<String>) {
	runApplication<DelibirdMetaApplication>(*args)
}

@Bean
fun json(): MappingJackson2JsonView {
	return MappingJackson2JsonView(ObjectMapper())
}
