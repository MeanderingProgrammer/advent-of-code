plugins {
    application
}

repositories {
    mavenCentral()
}

dependencies { 
    implementation(project(":lib"))
    implementation("com.google.guava:guava:32.1.3-jre")
    compileOnly("org.projectlombok:lombok:1.18.30")
    annotationProcessor("org.projectlombok:lombok:1.18.30")
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

sourceSets {
    named("main") {
        java.srcDir("src")
    }
}

application {
    mainClass.set("Solver")
}
