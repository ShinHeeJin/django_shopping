---
description: about auth
---

# 사용자 인증

about auth

{% api-method method="get" host="https://localhost" path="/api\_v1/auth/user" %}
{% api-method-summary %}
CREATE USER
{% endapi-method-summary %}

{% api-method-description %}

{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="type" type="string" required=true %}
sign-in type \( M, K, G, F \)
{% endapi-method-parameter %}

{% api-method-parameter name="email" type="string" required=true %}

{% endapi-method-parameter %}

{% api-method-parameter name="password" type="string" required=false %}
if sns password is null
{% endapi-method-parameter %}

{% api-method-parameter name="serviceAgree" type="boolean" required=true %}

{% endapi-method-parameter %}

{% api-method-parameter name="privacyAgree" type="boolean" required=true %}

{% endapi-method-parameter %}

{% api-method-parameter name="marketingAgree" type="boolean" required=true %}

{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
create user result \( must be Y \)
{% endapi-method-response-example-description %}

```
{
    "result":"Y"
}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

