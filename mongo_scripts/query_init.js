// create role
db.createRole(
  {
    role: "adminUserCC",
    roles: [],
    privileges:[
    	{
    		resource: { db: "costcontroldev" , collection: "" },
         	actions: [ "insert", "update", "find","remove", "createCollection", "dbStats", "collStats", "listCollections" ]
    	}
    ]
  }
)

// create user
db.createUser({user: "userccdev", pwd: "", roles: ["adminUserCC"]})

// update role
db.updateRole(
  "adminUserCC",
  {
    privileges:[
    	{
    		resource: { db: "costcontroldev" , collection: "" },
         	actions: [ "insert", "update", "find","remove", "createCollection", "dbStats", "collStats", "listCollections" ]
    	}
    ]
  }
)