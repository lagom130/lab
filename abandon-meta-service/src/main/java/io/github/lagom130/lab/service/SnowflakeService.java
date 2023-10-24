package io.github.lagom130.lab.service;


import io.github.lagom130.lab.globalResponse.BizException;
import io.github.lagom130.lab.leaf.IDGen;
import io.github.lagom130.lab.leaf.common.PropertyFactory;
import io.github.lagom130.lab.leaf.common.Result;
import io.github.lagom130.lab.leaf.common.ZeroIDGen;
import io.github.lagom130.lab.leaf.snowflake.SnowflakeIDGenImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.Properties;

@Service("SnowflakeService")
public class SnowflakeService {
    private Logger logger = LoggerFactory.getLogger(SnowflakeService.class);

    private IDGen idGen;

    public SnowflakeService() {
        Properties properties = PropertyFactory.getProperties();
        boolean flag = true;
//        boolean flag = Boolean.parseBoolean(properties.getProperty(Constants.LEAF_SNOWFLAKE_ENABLE, "true"));
        if (flag) {
//            String zkAddress = properties.getProperty(Constants.LEAF_SNOWFLAKE_ZK_ADDRESS);
//            int port = Integer.parseInt(properties.getProperty(Constants.LEAF_SNOWFLAKE_PORT));
            idGen = new SnowflakeIDGenImpl("", 8848);
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
