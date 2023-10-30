package io.github.lagom130.lab.mapper;

import io.github.lagom130.lab.entity.Catalog;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

/**
 * <p>
 *  Mapper 接口
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@Mapper
public interface CatalogMapper extends BaseMapper<Catalog> {

}
