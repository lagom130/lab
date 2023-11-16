package io.github.lagom130.lab.abandon.order;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
public class CanaryOrderApplication {

    public static void main(String[] args) {
        SpringApplication.run(CanaryOrderApplication.class, args);
    }

}
