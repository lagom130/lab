package io.github.lagom130.lab.codegen.work;

import com.baomidou.mybatisplus.generator.AutoGenerator;
import com.baomidou.mybatisplus.generator.config.DataSourceConfig;
import com.baomidou.mybatisplus.generator.config.rules.NamingStrategy;
import com.baomidou.mybatisplus.generator.engine.FreemarkerTemplateEngine;

/**
 * MBP代码生成器
 *
 * @author lujc
 * @date 2023/7/14.
 */
public class MySqlGeneratorGX extends BaseGenerator {
    private static final String AUTHOR = "lujc";
    private static final String OUTPUT_DIR = "D://codeGen//x";
    /**
     * 数据源配置
     */
    private static final DataSourceConfig DATA_SOURCE_CONFIG = new DataSourceConfig
//            .Builder("jdbc:mysql://mysql-master:3306/wso2is_db?characterEncoding=utf-8&autoReconnect=true&serverTimezone=Asia/Shanghai", "bigdata", "123@abcd")
//            .build();
            .Builder("jdbc:mysql://10.10.32.6:3306/ls_quality?characterEncoding=utf-8&autoReconnect=true&serverTimezone=Asia/Shanghai", "wingtest", "123@abcd")
            .build();
    public static void main(String[] args) {
        AutoGenerator generator = new AutoGenerator(DATA_SOURCE_CONFIG);
        generator.strategy(strategyConfig()
                        .entityBuilder()
                .naming(NamingStrategy.underline_to_camel)
                .columnNaming(NamingStrategy.underline_to_camel)
                        .formatFileName("%sEntity")
                        .enableLombok()
                        .enableTableFieldAnnotation()
                .serviceBuilder()
                .formatServiceFileName("%sDao")
                .formatServiceImplFileName("%sDaoImpl")
                .build());

        generator.global(globalConfig()
                        .author(AUTHOR)
                        .fileOverride()
                        .outputDir(OUTPUT_DIR)
                .build());
        generator.packageInfo(packageConfig()
                        .parent("com.wingconn.bd.executor")
                .entity("entity.exquality")
                .mapper("mapper.exquality")
                        .service("dao.exquality")
                        .serviceImpl("dao.exquality.impl")
                        .xml("mappings.exquality")
                .build()
        );
        generator.execute(new FreemarkerTemplateEngine());


    }
}
