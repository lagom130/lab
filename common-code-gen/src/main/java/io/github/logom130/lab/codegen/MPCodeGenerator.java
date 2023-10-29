package io.github.logom130.lab.codegen;

import com.baomidou.mybatisplus.generator.FastAutoGenerator;
import com.baomidou.mybatisplus.generator.config.GlobalConfig;
import com.baomidou.mybatisplus.generator.config.OutputFile;
import com.baomidou.mybatisplus.generator.engine.VelocityTemplateEngine;

import java.util.Collections;
import java.util.function.BiConsumer;
import java.util.function.Function;

public class MPCodeGenerator {
    public static void main(String[] args) {
        String url = "jdbc:mysql://127.0.0.1:3306/abandon_nydus?serverTimezone=Asia/Shanghai";
        String username = "root";
        String password = "Qwerty!2345";
        String author = "lagom";
        String projectPath = "C://MyProjects\\lab\\abandon-nydus-service";

        String packageParent = "io.github.lagom130.lab";
        String module = "";

        String xmlPath = projectPath+"\\src\\main\\resources\\mapper";
        String fullCodePath = projectPath+"\\src\\main\\java\\";


        FastAutoGenerator.create(url, username, password)
                .globalConfig(builder -> {
                    builder.author(author) // 设置作者
//                            .enableSwagger() // 开启 swagger 模式
                            .outputDir(fullCodePath); // 指定输出目录
                })
                .packageConfig(builder -> {
                    builder.parent(packageParent) // 设置父包名
//                            .moduleName(module) // 设置父包模块名
                            .pathInfo(Collections.singletonMap(OutputFile.xml, xmlPath)); // 设置mapperXml生成路径
                })
                .strategyConfig(builder -> {
                    builder.addExclude("undo_log") // 设置需要生成的表名
//                            .addTableSuffix("_tbl")
                    ; // 设置过滤表后缀
                })
                .templateEngine(new VelocityTemplateEngine()) // 使用Freemarker引擎模板，默认的是Velocity引擎模板
                .execute();
    }
}
