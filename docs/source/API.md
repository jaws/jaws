# API

## Adding new variables to an existing network
___

Each network has a list of variables (from raw file) that are known to `JAWS` at:
```html
jaws/resources/{network_name}/columns.txt
```

where 'network_name' is the name of newtork lke 'gcnet', 'promice', etc.
 
If you want to modify JAWS and add new variables to a network, you need to modify following 3 files i.e.
```html
jaws/resources/{network_name}/columns.txt
```

```html
jaws/resources/{network_name}/ds.json
```

```html
jaws/resources/{network_name}/encoding.json
```

In this example, we will add two new variables ('Sensible Heat Flux' and 'Latent Heat Flux') to PROMICE.

**Step 1**:  Add *variable names* to **columns.txt** of that network in **same order** as they are in raw file.
In our example raw file, 'sensible_heat_flux' comes after 'wind_direction' and is followed by 'latent_heat_flux'. 
So, we will add new variables like this:

![](http://jaws.ess.uci.edu/jaws/img/add_new_var1.png)

**Step 2**: Next, we will populate *attributes information* for the newly added variables in **ds.json** as following:

![](http://jaws.ess.uci.edu/jaws/img/add_new_var2.png)

**Step 3**: Then, we will add the encoding information in **encoding.json** as below:

![](http://jaws.ess.uci.edu/jaws/img/add_new_var3.png)

**Step 4**: The final step is only for `AAWS, GCNet and PROMICE` networks. You will need to update the count
of variables in **jaws/common.py**. Since we have added two variable, so we will update the 
`len(input_file_vars)` from 44 to 46 as following:

![](http://jaws.ess.uci.edu/jaws/img/add_new_var4.png)

If you have trouble following the above or have any questions, please open up an issue
on [Github](https://github.com/jaws/jaws/issues)

## Add new network

If your network is not in the list [here](Supported%20Networks.html) and you would like it to be supported by **JAWS**, 
please open an issue on [Github](https://github.com/jaws/jaws/issues) or contact *Charlie Zender* at <zender@uci.edu>
