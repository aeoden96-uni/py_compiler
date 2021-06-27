# IP_zadaca

## Contributors
```sh
Matija Fabek
Mateo Martinjak 
```
## Literals


Name | Real value
------------ | -------------
TRUE | 1
UNDEFINED | 0
FALSE | -1


## Variable types

Type name | Holds | Description | Example
------------ | ------------- | ------------- | -------------
int | integer | starts with a small letter | ``` c= 2;```
string | string | starts with a small letter | ``` c= "id";```
bool | integer | 3val logic,starts with capital letter | ```R= UNDEFINED; ```
list | list | starts with capital letter 'L' | ```L1 = [1,2,3]; ```



## Examples

1. Arithmetic

```cpp
//arithmetic
c= 2*8;
d= 3-6;
e=  2;
print(c - (d + e));

//Ispisujem: 17
```

2. Type manipulation

```cpp
//type manipulation

idFirst= 2250;
idSecond= 5078;
shift="2";

id= (string)idFirst + (string)(idSecond + (int)shift);
a = "Your ID is ";

print(a + id);
//Ispisujem: Your ID is 22505080
```

3. Logic manipulation

```cpp

d= 0;
A= UNDEFINED or TRUE;//A is TRUE
B= not TRUE or d==0 and TRUE; //B is TRUE,and has priority

if (B and A)
    d=1;
print(d);

//Ispisujem: 1
```

4.a Simple list and conversion 'LIST -> variables'

```cpp

//left side can be: env_function that returns a list, LIST or LIST_VAR

v,p = getCoord();
print(p);

L = [ 20 + 4 , 20 + 6 ];
v,p = L;
print(p);

v,p = [2,4];
print(p);

//IZ OKOLINE DOBIVENE koordinate: [2,15]
//Ispisujem: 15
//Ispisujem: 26
//Ispisujem: 4
```
