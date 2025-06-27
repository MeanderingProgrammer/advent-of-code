plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

rootProject.name = "advent-of-code"

include("lib")
project(":lib").projectDir = file("commons/java")

include("2019-18")
project(":2019-18").projectDir = file("2019/18")

include("2019-20")
project(":2019-20").projectDir = file("2019/20")

include("2021-01")
project(":2021-01").projectDir = file("2021/01")
