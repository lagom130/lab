package io.github.lagom130.lab.abandon.biz;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
public class CanaryBizApplication {

    public static void main(String[] args) {
        SpringApplication.run(CanaryBizApplication.class, args);
    }

}
