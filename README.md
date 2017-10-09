# JAWS: Justified Automated Weather Station

JAWS is a scientiﬁc software workﬂow to ingest Level 2 (L2) data in the multiple formats now distributed, harmonize it into a common format, and deliver value-added Level3 (L3) output suitable for distribution by the network operator, analysis by the researcher, and curation by the data center. 


## What does it do?

#### 1) Standardization

Convert L2 data (usually ASCII tables) into a netCDF-based L3 format compliant with metadata conventions (Climate-Forecast and ACDD) that promote automated discovery and
analysis. 

#### 2) Adjustment

Include value-added L3 features like the Retrospective, Iterative, Geometry-Based (RIGB) tilt angle and direction corrections, solar angles, and standardized quality flags. 

#### 3) API

Provide a scriptable API to extend the initial L2-to-L3 conversion to newer AWS-like networks and instruments.


## Resources

* [API Reference](https://github.com/jaws/JustifiedAWS/blob/master/API.md)
* [Release Notes](https://github.com/jaws/JustifiedAWS/releases)
* [Gallery](https://github.com/jaws/JustifiedAWS/wiki/Gallery)
* [Examples](https://)


## Full Documentation

See the [Wiki](https://github.com/jaws/JustifiedAWS/wiki/) for full documentation, examples, operational details and other information.


## Installation


## Usage


<!---

## Hello World!

Code to be isolated is wrapped inside the run() method of a HystrixCommand similar to the following:

```java
public class CommandHelloWorld extends HystrixCommand<String> {

    private final String name;

    public CommandHelloWorld(String name) {
        super(HystrixCommandGroupKey.Factory.asKey("ExampleGroup"));
        this.name = name;
    }

    @Override
    protected String run() {
        return "Hello " + name + "!";
    }
}
```

This command could be used like this:

```java
String s = new CommandHelloWorld("Bob").execute();
Future<String> s = new CommandHelloWorld("Bob").queue();
Observable<String> s = new CommandHelloWorld("Bob").observe();
```

More examples and information can be found in the [How To Use](https://github.com/Netflix/Hystrix/wiki/How-To-Use) section.

Example source code can be found in the [hystrix-examples](https://github.com/Netflix/Hystrix/tree/master/hystrix-examples/src/main/java/com/netflix/hystrix/examples) module.

-->

## Build

To build:

```

```


## Run Demo

To run a [demo](https://github.com/jaws/JustifiedAWS/tree/master/) do the following:

```
$ git clone 

```

You will see output similar to the following:

```

```



## Bugs and Feedback

For bugs, questions and discussions please use the [GitHub Issues](https://github.com/jaws/JustifiedAWS/issues).

 
## Copyright and License

