# aicodesign (Java)

**Provenance and review tracking for AI-generated code.**

In fast-moving environments, using LLMs to generate code accelerates development, but it introduces varying levels of risk. `aicodesign` provides lightweight Java annotations to explicitly mark the review status and trust boundaries of AI-generated code running in production.

## Requirements

- **Java:** 25+

## Installation

Add the following dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>dev.aicodesign</groupId>
    <artifactId>aicodesign</artifactId>
    <version>0.1.0-SNAPSHOT</version>
</dependency>
```

## Usage Examples

```java
import dev.aicodesign.AiDraft;
import dev.aicodesign.AiBlackbox;
import dev.aicodesign.AiCoSigned;

public class OrderService {

    // Tier 3: Pure AI Draft
    @AiDraft(ticket="HFT-101")
    public void calculateMomentumAlpha(Object prices) {
        // Unreviewed logic and tests
    }

    // Tier 2: AI Blackbox
    @AiBlackbox(ticket="HFT-102", notes="Tests verify strict output boundaries")
    public void parseExchangeFeed(Object payload) {
        // Logic is unreviewed, but a human vetted the test harness
    }

    // Tier 1: Co-Signed Code
    @AiCoSigned(reviewer="alice.dev", ticket="HFT-103")
    public void updateOrderBook(Object book, Object newOrders) {
        // A human has audited the logic and tests
    }
}
```

## Introspection

All annotations have `RUNTIME` retention, making it easy to build CI/CD guardrails or runtime telemetry (e.g., using AOP or reflection) to track AI code execution:

```java
import dev.aicodesign.AiCoSigned;
import java.lang.reflect.Method;

public class IntrospectionExample {
    public static void main(String[] args) throws Exception {
        Method method = OrderService.class.getMethod("updateOrderBook", Object.class, Object.class);
        if (method.isAnnotationPresent(AiCoSigned.class)) {
            AiCoSigned annotation = method.getAnnotation(AiCoSigned.class);
            System.out.println("Reviewer: " + annotation.reviewer()); // Output: alice.dev
        }
    }
}
```

## Note on Runtime Telemetry
Unlike the Python version which intercepts the method call automatically via decorators, the Java implementation provides the **metadata annotations**. To automatically intercept method calls and emit runtime warnings (e.g., for `@AiDraft`), you will need to apply an AOP framework like **Spring AOP** or **AspectJ** that targets these annotations.
