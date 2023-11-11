package io.github.lagom130.lab

import com.baomidou.mybatisplus.generator.FastAutoGenerator
import com.baomidou.mybatisplus.generator.config.GlobalConfig
import com.baomidou.mybatisplus.generator.config.OutputFile
import com.baomidou.mybatisplus.generator.config.PackageConfig
import com.baomidou.mybatisplus.generator.config.StrategyConfig
import com.baomidou.mybatisplus.generator.engine.VelocityTemplateEngine
import java.util.*

object MPCodeGenerator {
    @JvmStatic
    fun main(args: Array<String>) {
        val url = "jdbc:mysql://127.0.0.1:3306/abandon_nydus?serverTimezone=Asia/Shanghai"
        val username = "root"
        val password = "Qwerty!2345"
        val author = "lagom"
        val projectPath = "C://MyProjects\\lab\\abandon-nydus-service"
        val packageParent = "io.github.lagom130.lab"
        val module = ""
        val xmlPath = "$projectPath\\src\\main\\resources\\mapper"
        val fullCodePath = "$projectPath\\src\\main\\java\\"
        FastAutoGenerator.create(url, username, password)
                .globalConfig { builder: GlobalConfig.Builder ->
                    builder.author(author) // 设置作者
                            //                            .enableSwagger() // 开启 swagger 模式
                            .enableKotlin()
                            .outputDir(fullCodePath) // 指定输出目录
                }
                .packageConfig { builder: PackageConfig.Builder ->
                    builder.parent(packageParent) // 设置父包名
                            //                            .moduleName(module) // 设置父包模块名
                            .pathInfo(Collections.singletonMap(OutputFile.xml, xmlPath)) // 设置mapperXml生成路径
                }
                .strategyConfig { builder: StrategyConfig.Builder ->
                    builder.addExclude("undo_log") // 设置需要生成的表名
                    //                            .addTableSuffix("_tbl")
                    // 设置过滤表后缀
                }
                .templateEngine(VelocityTemplateEngine()) // 使用Freemarker引擎模板，默认的是Velocity引擎模板
                .execute()
    }
}
