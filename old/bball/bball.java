for (int i = 0; i < ballCount; i++)  
{  
	for (int j = i + 1; j < ballCount; j++)  
	{  
		if (balls[i].colliding(balls[j]))  
		{
			balls[i].resolveCollision(balls[j]);
		}
	}
}
//------------------------------------------------------------------------
public boolean colliding(Ball ball)
{
	float xd = position.getX() - ball.position.getX();
	float yd = position.getY() - ball.position.getY();

	float sumRadius = getRadius() + ball.getRadius();
	float sqrRadius = sumRadius * sumRadius;

	float distSqr = (xd * xd) + (yd * yd);

	if (distSqr <= sqrRadius)
	{
		return true;
	}

	return false;
}
//------------------------------------------------------------------------
public void resolveCollision(Ball ball)
{
	// get the mtd
	Vector2d delta = (position.subtract(ball.position));
	float d = delta.getLength();
	// minimum translation distance to push balls apart after intersecting
	Vector2d mtd = delta.multiply(((getRadius() + ball.getRadius())-d)/d); 


	// resolve intersection --
	// inverse mass quantities
	float im1 = 1 / getMass(); 
	float im2 = 1 / ball.getMass();

	// push-pull them apart based off their mass
	position = position.add(mtd.multiply(im1 / (im1 + im2)));
	ball.position = ball.position.subtract(mtd.multiply(im2 / (im1 + im2)));

	// impact speed
	Vector2d v = (this.velocity.subtract(ball.velocity));
	float vn = v.dot(mtd.normalize());

	// sphere intersecting but moving away from each other already
	if (vn > 0.0f) return;

	// collision impulse
	float i = (-(1.0f + Constants.restitution) * vn) / (im1 + im2);
	Vector2d impulse = mtd.multiply(i);

	// change in momentum
	this.velocity = this.velocity.add(impulse.multiply(im1));
	ball.velocity = ball.velocity.subtract(impulse.multiply(im2));
}
