package io.github.lagom130.lab.service;


import com.alibaba.nacos.api.NacosFactory;
import com.alibaba.nacos.api.naming.NamingService;
import com.alibaba.nacos.api.naming.pojo.Instance;
import io.github.lagom130.lab.globalResponse.BizException;
import io.github.lagom130.lab.leaf.IDGen;
import io.github.lagom130.lab.leaf.common.PropertyFactory;
import io.github.lagom130.lab.leaf.common.Result;
import io.github.lagom130.lab.leaf.common.ZeroIDGen;
import io.github.lagom130.lab.leaf.snowflake.SnowflakeIDGenImpl;
import jakarta.annotation.Resource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Properties;

@Service("SnowflakeService")
public class SnowflakeService {
    private Logger logger = LoggerFactory.getLogger(SnowflakeService.class);

    private IDGen idGen;

    @Value("${spring.application.name}")
    private String serviceName;

    public SnowflakeService() {

//        Properties properties = PropertyFactory.getProperties();
//        boolean flag = Boolean.parseBoolean(properties.getProperty(Constants.LEAF_SNOWFLAKE_ENABLE, "true"));
        boolean flag = true;
        if (flag) {
            idGen = new SnowflakeIDGenImpl(0);
            if(idGen.init()) {
                logger.info("Snowflake Service Init Successfully");
            } else {
                throw new BizException(500, "Snowflake Service Init Fail");
            }
        } else {
            idGen = new ZeroIDGen();
            logger.info("Zero ID Gen Service Init Successfully");
        }
    }

    public Result getId(String key) {
        return idGen.get(key);
    }
}
