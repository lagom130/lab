package io.github.lagom130.lab.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import io.github.lagom130.lab.entity.Audit;
import io.github.lagom130.lab.vo.AuditDetailVo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * <p>
 *  Mapper 接口
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@Mapper
public interface OrgAuditMapper extends BaseMapper<Audit> {
}
