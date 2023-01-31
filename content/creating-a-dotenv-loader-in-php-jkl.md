---
cover_image: https://res.cloudinary.com/practicaldev/image/fetch/s--Oqq-ofCi--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/g4vrvcah3t86ib1s8r2h.png
description: From the list of some of the most common libraries that are heavily used
  in a PHP framework project...
id: 1043472
published: true
published_at: '2022-04-10T06:46:27.140Z'
tags:
- php
- symfony
- phpunit
- backend
title: Creating a DotEnv Loader in PHP
---
From the list of some of the most common libraries that are heavily used in a PHP framework project is DotEnv. The package that is used to load .env variables into the program from .env file. These env values are usually secrets patched for each environment and there is a subtle security issue in the process.
Anyways, in this blog today, we gonna build a DotEnv class from scratch.

## Getting started

Let's create a sample .env file to be read and include variables with all cornered cases.

**.env**

```env
# A PostgreSQL connection string
DATABASE_URL=postgres://localhost:5432/noah_arc

# The lowest level of logs to output
LOG_LEVEL=debug

# The environment to run the application in
NODE_ENV=development

# The HTTP port to run the application on
PORT=8080

# The secret to encrypt session IDs with
SESSION_SECRET=development

API_KEY="hwhhwhshs6585gahwhgwuwjwusuhs"

APP_KEY=VGhpcyBpcyBhbiBlbmNvZGVkIHN0cmluZw==
APP_DESCRIPTION="This is a long sentence with whitespace and characters "
```

## Final Code

**DotEnv.php**

```php
<?php
namespace PHPizer\DotEnv;

use Exception;

class DotEnv
{
    protected $path;
    public $variables;

    public function __construct(string $path)
    {
        if (!file_exists($path)) {
            throw new Exception("File not found: {$path}");
        }
        $this->path = $path;
    }

    public function load(): void
    {
        if (!is_readable($this->path)) {
            throw new Exception("File not readable: {$this->path}");
        }

        $lines = file($this->path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        foreach ($lines as $line) {
            if (strpos(trim($line), '#') === 0) {
                continue;
            }

            list($name, $value) = explode('=', $line, 2);
            $name = trim($name);
            $value = trim($value,"\x00..\x1F\"");
            $this->variables[$name] = $value;

            if (!array_key_exists($name, $_SERVER) && !array_key_exists($name, $_ENV)) {
                putenv(sprintf('%s=%s', $name, $value));
                $_ENV[$name] = $value;
                $_SERVER[$name] = $value;
            }
        }
    }
}

```

Dotenv class create an object with path and if file doesn't exists throws an Exception. Object needs to called with load() fn which checks if file is readable and then tokenize each into key-value pair if not blank space or comment and set as env variable.

## Testing


```php
<?php

declare(strict_types=1);

namespace Tests;

use PHPizer\DotEnv\DotEnv;
use PHPUnit\Framework\TestCase;

final class DotEnvTest extends TestCase
{
    protected $path;
    protected DotEnv $dotEnv;


    public function testLoadEnv(): void
    {
        $this->path = "./tests/test.env";
        $this->dotEnv = new DotEnv($this->path);
        $this->assertNull($this->dotEnv->variables);
        $this->dotEnv->load();
        $envArray = [
            "DATABASE_URL" => "postgres://localhost:5432/noah_arc",
            "LOG_LEVEL" => "debug",
            "NODE_ENV" => "development",
            "PORT" => 8080,
            "SESSION_SECRET" => "development",
            "API_KEY" => "hwhhwhshs6585gahwhgwuwjwusuhs",
            "APP_KEY" => "VGhpcyBpcyBhbiBlbmNvZGVkIHN0cmluZw==",
            "APP_DESCRIPTION" => "This is a long sentence with whitespace and characters "
        ];
        foreach ($this->dotEnv->variables as $key => $value) {
            $this->assertEquals($value, $_ENV[$key]);
            $this->assertEquals($value, $_SERVER[$key]);
            $this->assertEquals($value, $envArray[$key]);
        }
        $this->assertTrue(true);
    }
}

```

DotEnvTest tests values if every variables are properly parsed out of the env file.

## References

- [symfony/dotenv](https://github.com/symfony/dotenv)
