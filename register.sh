#!/usr/bin/bash
curl -X POST http://localhost:5000/register\
	-H "Content-Type: application/json"\
	-d "{"username": "boniface","email":"boniface@yahoo.com","password":"secure12345"}"
