package dev.aicodesign;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Tier 2 (Medium Risk): AI Blackbox.
 * 0 reviews on code logic, but bounded/verified by human-reviewed unit tests.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE, ElementType.METHOD, ElementType.CONSTRUCTOR})
public @interface AiBlackbox {
    String author() default "LLM";
    String ticket() default "";
    String notes() default "";
}
