package io.github.lagom130.lab.enums;

import com.fasterxml.jackson.annotation.JsonValue;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Stream;

public interface IBaseEnum <T>{
    // Initialize the enum with a code and description
    default void init(T code, String desc) {
        EnumContainer.putEnum(this, code, desc);
    }

    // Get the code of the enum
    @JsonValue
    default T getCode() {
        return EnumContainer.getEnum(this).getCode();
    }

    // Get the description of the enum
    default String getDesc() {
        return EnumContainer.getEnum(this).getDesc();
    }

    // Get an enum by its code
    @SuppressWarnings("unchecked")
    static <T, R extends IBaseEnum<T>> R getByCode(Class<? extends IBaseEnum<T>> clazz, T code) {
        return Stream.of(clazz.getEnumConstants())
                .filter(tEnumBean -> tEnumBean.getCode().equals(code))
                .map(v -> (R)v)
                .findFirst()
                .orElse(null);
    }

    // Get an enum by its description
    @SuppressWarnings("unchecked")
    static <T, R extends IBaseEnum<T>> R getByDesc(Class<? extends IBaseEnum<T>> clazz, String desc) {
        return Stream.of(clazz.getEnumConstants())
                .filter(tEnumBean -> tEnumBean.getDesc().equalsIgnoreCase(desc))
                .map(v -> (R)v)
                .findFirst()
                .orElse(null);
    }


    // The enum container
    class EnumContainer {
        // Create a map to store the enum
        private static final Map<IBaseEnum, EnumBean> ENUM_MAP = new ConcurrentHashMap<>();

        // Put an enum into the map
        public static <T> void putEnum(IBaseEnum<T> baseEnum, T code, String desc) {
            ENUM_MAP.put(baseEnum, new EnumBean(code, desc));
        }

        // Get an enum from the map
        static <K extends IBaseEnum<T>, T> EnumBean<T> getEnum(K dict) {
            return ENUM_MAP.get(dict);
        }
    }
    // The enum bean
    class EnumBean<T> {
        // Store the code and description of the enum
        private T code;
        private String desc;

        public EnumBean(T code, String desc) {
            this.code = code;
            this.desc = desc;
        }

        // Get the code of the enum
        public T getCode() {
            return code;
        }

        // Get the description of the enum
        public String getDesc() {
            return desc;
        }
    }
}