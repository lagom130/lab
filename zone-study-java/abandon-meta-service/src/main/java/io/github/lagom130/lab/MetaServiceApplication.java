package io.github.lagom130.lab;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@SpringBootApplication
public class MetaServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(MetaServiceApplication.class, args);
    }

}
