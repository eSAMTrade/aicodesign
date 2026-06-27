package dev.aicodesign;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Tier 3 (High Risk): Pure AI draft.
 * 0 reviews on code, 0 reviews on tests.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE, ElementType.METHOD, ElementType.CONSTRUCTOR})
public @interface AiDraft {
    String author() default "LLM";
    String ticket() default "";
    String notes() default "";
}
