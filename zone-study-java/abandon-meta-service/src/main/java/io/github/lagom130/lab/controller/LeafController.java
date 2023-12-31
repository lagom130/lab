//package io.github.lagom130.lab.controller;
//
//import io.github.lagom130.lab.globalResponse.BizException;
//import io.github.lagom130.lab.leaf.common.Result;
//import io.github.lagom130.lab.leaf.common.Status;
//import io.github.lagom130.lab.service.SnowflakeService;
//import jakarta.annotation.Resource;
//import org.slf4j.Logger;
//import org.slf4j.LoggerFactory;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.web.bind.annotation.PathVariable;
//import org.springframework.web.bind.annotation.RequestMapping;
//import org.springframework.web.bind.annotation.RestController;
//
//@RestController
//public class LeafController {
//    private Logger logger = LoggerFactory.getLogger(LeafController.class);
//
////    @Autowired
////    private SegmentService segmentService;
////    @Resource
////    private SnowflakeService snowflakeService;
//
////    @RequestMapping(value = "/api/segment/get/{key}")
////    public String getSegmentId(@PathVariable("key") String key) {
////        return get(key, segmentService.getId(key));
////    }
//
////    @RequestMapping(value = "/api/snowflake/get/{key}")
////    public String getSnowflakeId(@PathVariable("key") String key) {
////        return get(key, snowflakeService.getId(key));
////    }
//
//    private String get(@PathVariable("key") String key, Result id) {
//        Result result;
//        if (key == null || key.isEmpty()) {
//            throw new BizException(500, "no key");
//        }
//        result = id;
//        if (result.getStatus().equals(Status.EXCEPTION)) {
//            throw new BizException(500, result.toString());
//        }
//        return String.valueOf(result.getId());
//    }
//}
