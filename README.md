# pyxdiag

pyxdiag provides an integrated interface of diag series -(block|seq|act|nw|rack|packet)diag-.

```
> python pyxdiag.py example.diag
```

## Background

diag series are very usefull tools but the user needs to write "diagram directive comment"(e.g. blockdiag {...}, seqdiag {...}) and has to use the appropriate tool as below:


http://blockdiag.com/en/blockdiag/examples.html#simple-diagram

```a.diag
blockdiag {
   A -> B -> C -> D;
   A -> E -> F -> G;
}
```

```generation_command
> blockdiag a.diag
```


http://blockdiag.com/en/seqdiag/examples.html#simple-diagram

```b.diag
seqdiag {
  browser  -> webserver [label = "GET /index.html"];
  browser <-- webserver;
  browser  -> webserver [label = "POST /blog/comment"];
              webserver  -> database [label = "INSERT comment"];
              webserver <-- database;
  browser <-- webserver;
}
```

```generation_command
> seqdiag b.diag
```

However, if a.diag and b.diag include "diagram directive comment" , the appropriate tool can be estimated. This means the user needs to write "diagram directive comment" but does not need to swtich the tools.

So, pyxdiag does it. 