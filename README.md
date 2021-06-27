# IP_zadaca

https://github.com/aeoden96/IP_zadaca

## Contributors
```sh
Matija Fabek
Mateo Martinjak 
```
## Environment functions: they are implemented in Turtle,  their implementation should function as a 'black box' to the user 


Function | To/from environment | Description | Example
------------ | ------------- | ------------- | -------------
getCoord | FROM | gets list with x,y coords | ``` x,y= getCoord();```
getOrientation | FROM | get orientation | ``` r=getOrientation();```
setPower | TO | sets turtle power | ```setPower(TRUE); ```
setSpeed | TO | sets turtle speed  | ```setSpeed(2); ```
setSteps | TO | sets turtle steps | ```setSteps(50); ```
setRot | TO | sets turtle rotation | ```setRot(rot); ```

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

4.a Simple list 
```cpp

Lot = [4,8];

if (4 in Lot)
    print("T");

//Ispisujem: T
```   
4.b List conversion 'LIST -> variables'

```cpp

//left side can be: env_function that returns a list, LIST or LIST_VAR

v,p = getCoord();
print(p);

L = [ 20 + 4 , 20 + 6 ];
v,p = L;
print(p);

v,p = [2,4];
print(p);

print(L[0]);

//IZ OKOLINE DOBIVENE koordinate: [2,15]
//Ispisujem: 15
//Ispisujem: 26
//Ispisujem: 4
//Ispisujem: 24
```

5. Tutle example

```cpp
print("program pocinje s radom");
rot = 90;
x,y= getCoord();
r=getOrientation();


setPower(TRUE);
setSpeed(2);

for (i=0; i < 8 ; i++){
    
    
    x,y= getCoord();
    r=getOrientation();

    setSteps(50);
    setRot(rot);

    if (i == 4) rot =  rot-45;
    if (i == 4) break;
}

print("program gotov s radom");
```
