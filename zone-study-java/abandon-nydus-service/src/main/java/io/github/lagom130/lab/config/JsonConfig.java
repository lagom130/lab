//package io.github.lagom130.lab.config;
//
//import com.fasterxml.jackson.annotation.JsonAutoDetect;
//import com.fasterxml.jackson.annotation.PropertyAccessor;
//import com.fasterxml.jackson.databind.*;
//import com.fasterxml.jackson.databind.introspect.JacksonAnnotationIntrospector;
//import com.fasterxml.jackson.datatype.jdk8.Jdk8Module;
//import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
//import com.fasterxml.jackson.module.paramnames.ParameterNamesModule;
//import org.springframework.boot.jackson.JsonComponentModule;
//import org.springframework.context.annotation.Bean;
//import org.springframework.context.annotation.Configuration;
//
///**
// * @author lujc
// * @date 2023/10/31.
// */
//@Configuration
//public class JsonConfig {
//    @Bean
//    public ObjectMapper ObjectMapper(){
//        ObjectMapper objectMapper = new ObjectMapper()
//                .registerModule(new ParameterNamesModule())
//                .registerModule(new Jdk8Module())
//                .registerModule(new JavaTimeModule());
////        objectMapper.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
//        objectMapper.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL);
////        objectMapper.setAnnotationIntrospector(JacksonAnnotationIntrospector.nopInstance());
//        return objectMapper;
//    }
//}
