# final prototype of retargeting
## using direct mapping method
Test ENV:
- Blender ver: 4.2.4 LTS

---

Arco/Word Definition:
- Loc -> Location
- Rot -> Rotaion
- Scl -> Scale
- Tranfrom -> any of (Loc,Rot,Scl)
- host -> the original holder/owner of the info/data taken from.
- target -> the target/reciver of the info/data taken from the original owner/host


## What is direct mapping method
"direct mapping" taken advantage of *constrain* or *driver* to map/copy the Tranfrom of the *host* to the target bone.


## Problem with direct mapping method
constrain (specifically bone constrain) don't have an easy way to swap axis and change the euler-order to the approprite one.
and lack the ability to offset the Rot at any arbitrary angle.

driver do have a way to swap axis but it require quite a bit of setup. angle offset is the nightmare of it's own.
yes it doable but it's just a bunch of hardcoded math nightmare.

---

# after this commmit. I (Naythan Touqe) will be moving forward with a new "proxy parenting" techniqe.

