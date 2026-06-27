package dev.aicodesign;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Tier 1 (Lower Risk): AI code co-signed by a human.
 * 1 human review on code, 1+ human review on tests.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE, ElementType.METHOD, ElementType.CONSTRUCTOR})
public @interface AiCoSigned {
    String reviewer(); // MANDATORY
    String author() default "LLM";
    String ticket() default "";
    String notes() default "";
}
